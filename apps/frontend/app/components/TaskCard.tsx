/**
 * TaskCard component with smooth animations.
 *
 * Features:
 * - Smooth entry/exit animations
 * - Hover effects with scale transforms
 * - Completion animation with transitions
 * - Loading states with spinners
 * - Animated dropdown menu
 * - Status badge transitions
 */

"use client";

import { useState, useEffect } from "react";
import {
  CheckCircle,
  Circle,
  Trash2,
  Edit2,
  MoreVertical,
  Clock,
  Loader2,
} from "lucide-react";
import { toggleTask, deleteTask, updateTask } from "@/lib/api";
import { formatRelativeTime } from "@/lib/utils/date";
import { toast } from "@/lib/utils/toast";
import type { Task } from "@/lib/types";

interface TaskCardProps {
  task: Task;
  onUpdate?: () => void;
  onDelete?: () => void;
  index?: number; // For staggered animations
}

export function TaskCard({ task, onUpdate, onDelete, index = 0 }: TaskCardProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [showMenu, setShowMenu] = useState(false);
  const [isVisible, setIsVisible] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description || "");

  // Trigger entry animation on mount
  useEffect(() => {
    const timer = setTimeout(() => setIsVisible(true), index * 50);
    return () => clearTimeout(timer);
  }, [index]);

  // Close menu when clicking outside
  useEffect(() => {
    const handleClickOutside = () => setShowMenu(false);
    if (showMenu) {
      document.addEventListener("click", handleClickOutside);
      return () => document.removeEventListener("click", handleClickOutside);
    }
  }, [showMenu]);

  // Toggle completion status
  const handleToggleComplete = async () => {
    setIsLoading(true);
    try {
      await toggleTask(task.userId, task.id);
      onUpdate?.();
      toast.success(
        task.status === "completed"
          ? "Task marked as incomplete"
          : "Task marked as completed"
      );
    } catch (error) {
      console.error("Failed to update task:", error);
      toast.error("Failed to update task. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  // Delete task with confirmation
  const handleDelete = async () => {
    if (!confirm("Are you sure you want to delete this task?")) return;

    setIsDeleting(true);
    setIsLoading(true);

    // Wait for exit animation
    setTimeout(async () => {
      try {
        await deleteTask(task.userId, task.id);
        onDelete?.();
        toast.success("Task deleted successfully");
      } catch (error) {
        console.error("Failed to delete task:", error);
        toast.error("Failed to delete task. Please try again.");
        setIsDeleting(false);
      } finally {
        setIsLoading(false);
        setShowMenu(false);
      }
    }, 300);
  };

  // Toggle edit mode
  const handleEdit = () => {
    setShowMenu(false);
    setIsEditing(true);
    setEditTitle(task.title);
    setEditDescription(task.description || "");
  };

  // Save edited task
  const handleSaveEdit = async () => {
    if (!editTitle.trim()) {
      toast.error("Title cannot be empty");
      return;
    }

    setIsLoading(true);
    try {
      await updateTask(task.userId, task.id, {
        title: editTitle.trim(),
        description: editDescription.trim() || null,
      });
      setIsEditing(false);
      onUpdate?.();
      toast.success("Task updated successfully");
    } catch (error) {
      console.error("Failed to update task:", error);
      toast.error("Failed to update task. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  // Cancel editing
  const handleCancelEdit = () => {
    setIsEditing(false);
    setEditTitle(task.title);
    setEditDescription(task.description || "");
  };

  // Handle keyboard shortcuts in edit mode
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Escape") {
      handleCancelEdit();
    } else if (e.key === "Enter" && e.ctrlKey) {
      handleSaveEdit();
    }
  };

  return (
    <div
      className={`
        bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4
        transition-all duration-300 ease-out
        ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"}
        ${isDeleting ? "opacity-0 scale-95 -translate-x-full" : ""}
        ${task.status === "completed" ? "bg-gray-50/50 dark:bg-gray-700/50" : ""}
        hover:shadow-lg hover:scale-[1.02] hover:border-blue-300 dark:hover:border-blue-500
        group
        ${showMenu ? "relative z-50" : "relative z-0"}
      `}
      style={{
        transitionDelay: isVisible ? `${index * 50}ms` : "0ms",
      }}
    >
      <div className="flex items-start gap-3">
        {/* Completion Checkbox with Animation */}
        <button
          onClick={handleToggleComplete}
          disabled={isLoading}
          className={`
            mt-0.5 transition-all duration-200
            disabled:opacity-50 disabled:cursor-not-allowed
            ${isLoading ? "animate-pulse" : ""}
            ${task.status === "completed" ? "text-green-600" : "text-gray-400"}
            hover:text-blue-600 hover:scale-110
            active:scale-95
          `}
          aria-label={task.status === "completed" ? "Mark as incomplete" : "Mark as complete"}
        >
          {isLoading ? (
            <Loader2 className="w-5 h-5 animate-spin" aria-hidden="true" />
          ) : task.status === "completed" ? (
            <CheckCircle
              className="w-5 h-5 transition-transform duration-200 animate-[bounce_0.5s_ease-in-out]"
              aria-hidden="true"
            />
          ) : (
            <Circle
              className="w-5 h-5 transition-transform duration-200"
              aria-hidden="true"
            />
          )}
        </button>

        {/* Task Content with Smooth Transitions */}
        <div className="flex-1 min-w-0">
          {isEditing ? (
            /* Edit Mode */
            <div className="space-y-3">
              <input
                type="text"
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
                onKeyDown={handleKeyDown}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Task title"
                disabled={isLoading}
                autoFocus
              />
              <textarea
                value={editDescription}
                onChange={(e) => setEditDescription(e.target.value)}
                onKeyDown={handleKeyDown}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                placeholder="Task description (optional)"
                rows={2}
                disabled={isLoading}
              />
              <div className="flex gap-2">
                <button
                  onClick={handleSaveEdit}
                  disabled={isLoading}
                  className="px-4 py-2 bg-blue-600 dark:bg-blue-500 text-white rounded-md hover:bg-blue-700 dark:hover:bg-blue-600 disabled:opacity-50 text-sm font-medium"
                >
                  {isLoading ? "Saving..." : "Save"}
                </button>
                <button
                  onClick={handleCancelEdit}
                  disabled={isLoading}
                  className="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-md hover:bg-gray-300 dark:hover:bg-gray-600 disabled:opacity-50 text-sm font-medium"
                >
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            /* View Mode */
            <>
              {/* Title with Completion Animation */}
              <h3
                className={`
                  text-lg font-medium transition-all duration-300
                  ${task.status === "completed"
                    ? "line-through text-gray-500 dark:text-gray-400 opacity-75"
                    : "text-gray-900 dark:text-gray-100 group-hover:text-blue-600 dark:group-hover:text-blue-400"
                  }
                `}
              >
                {task.title}
              </h3>

              {/* Description with Fade */}
              {task.description && (
                <p className={`
                  text-sm mt-1 line-clamp-2 transition-colors duration-200
                  ${task.status === "completed" ? "text-gray-400 dark:text-gray-500" : "text-gray-600 dark:text-gray-400"}
                `}>
                  {task.description}
                </p>
              )}

              {/* Metadata with Animated Badges */}
              <div className="flex items-center gap-4 mt-3 text-xs text-gray-500">
                {/* Animated Status Badge */}
                <span
                  className={`
                    px-3 py-1 rounded-full font-medium
                    transition-all duration-300 ease-out
                    transform hover:scale-105
                    ${task.status === "completed"
                      ? "bg-green-100 text-green-800 shadow-sm"
                      : task.status === "in_progress"
                      ? "bg-yellow-100 text-yellow-800 shadow-sm"
                      : "bg-blue-50 text-blue-700 border border-blue-200"
                    }
                  `}
                >
                  {task.status === "completed" ? "✓ Completed" : task.status === "in_progress" ? "◐ In Progress" : "○ Pending"}
                </span>

                {/* Created Time with Icon Animation */}
                <span className="flex items-center gap-1 group/time">
                  <Clock
                    className="w-3 h-3 transition-transform duration-200 group-hover/time:rotate-12"
                    aria-hidden="true"
                  />
                  <span className="transition-colors duration-200 group-hover/time:text-gray-700">
                    {formatRelativeTime(task.createdAt)}
                  </span>
                </span>
              </div>
            </>
          )}
        </div>

        {/* Animated Action Menu - Always Visible (hidden during edit) */}
        {!isEditing && (
          <div className="relative" onClick={(e) => e.stopPropagation()}>
            <button
              onClick={() => setShowMenu(!showMenu)}
              className={`
                p-2 rounded-lg transition-all duration-200
                ${showMenu
                  ? "text-blue-600 bg-blue-50 scale-110"
                  : "text-gray-400 hover:text-gray-600 hover:bg-gray-100"
                }
                hover:scale-110 active:scale-95
              `}
              aria-label="Task actions"
              aria-expanded={showMenu}
              aria-haspopup="true"
            >
              <MoreVertical
                className={`w-5 h-5 transition-transform duration-200 ${
                  showMenu ? "rotate-90" : ""
                }`}
                aria-hidden="true"
              />
            </button>

          {/* Animated Dropdown Menu */}
          {showMenu && (
            <div
              className={`
                absolute right-0 mt-2 w-48
                bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-xl z-[100]
                animate-[slideIn_0.2s_ease-out]
                overflow-hidden
              `}
              role="menu"
            >
              <button
                onClick={handleEdit}
                className="
                  w-full flex items-center gap-3 px-4 py-3 text-sm
                  text-gray-700 dark:text-gray-300 hover:bg-blue-50 dark:hover:bg-blue-900/30 hover:text-blue-700 dark:hover:text-blue-400
                  transition-all duration-150
                  group/edit
                "
                role="menuitem"
              >
                <Edit2
                  className="w-4 h-4 transition-transform duration-200 group-hover/edit:scale-110"
                  aria-hidden="true"
                />
                <span>Edit Task</span>
              </button>
              <div className="border-t border-gray-100 dark:border-gray-700" />
              <button
                onClick={handleDelete}
                disabled={isLoading}
                className="
                  w-full flex items-center gap-3 px-4 py-3 text-sm
                  text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/30
                  transition-all duration-150
                  disabled:opacity-50 disabled:cursor-not-allowed
                  group/delete
                "
                role="menuitem"
              >
                {isLoading ? (
                  <Loader2 className="w-4 h-4 animate-spin" aria-hidden="true" />
                ) : (
                  <Trash2
                    className="w-4 h-4 transition-transform duration-200 group-hover/delete:scale-110 group-hover/delete:rotate-12"
                    aria-hidden="true"
                  />
                )}
                <span>Delete Task</span>
              </button>
            </div>
          )}
          </div>
        )}
      </div>
    </div>
  );
}
