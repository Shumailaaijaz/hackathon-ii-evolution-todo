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
import { toggleTask, deleteTask } from "@/lib/api";
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
        task.completed
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

  // Open edit modal (to be implemented)
  const handleEdit = () => {
    setShowMenu(false);
    // TODO: Open edit modal with task data
    toast.success("Edit feature coming soon!");
  };

  return (
    <div
      className={`
        bg-white border border-gray-200 rounded-lg p-4
        transition-all duration-300 ease-out
        ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"}
        ${isDeleting ? "opacity-0 scale-95 -translate-x-full" : ""}
        ${task.completed ? "bg-gray-50/50" : ""}
        hover:shadow-lg hover:scale-[1.02] hover:border-blue-300
        group
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
            ${task.completed ? "text-green-600" : "text-gray-400"}
            hover:text-blue-600 hover:scale-110
            active:scale-95
          `}
          aria-label={task.completed ? "Mark as incomplete" : "Mark as complete"}
        >
          {isLoading ? (
            <Loader2 className="w-5 h-5 animate-spin" aria-hidden="true" />
          ) : task.completed ? (
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
          {/* Title with Completion Animation */}
          <h3
            className={`
              text-lg font-medium transition-all duration-300
              ${task.completed
                ? "line-through text-gray-500 opacity-75"
                : "text-gray-900 group-hover:text-blue-600"
              }
            `}
          >
            {task.title}
          </h3>

          {/* Description with Fade */}
          {task.description && (
            <p className={`
              text-sm mt-1 line-clamp-2 transition-colors duration-200
              ${task.completed ? "text-gray-400" : "text-gray-600"}
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
                ${task.completed
                  ? "bg-green-100 text-green-800 shadow-sm"
                  : "bg-blue-50 text-blue-700 border border-blue-200"
                }
              `}
            >
              {task.completed ? "✓ Completed" : "○ Pending"}
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
        </div>

        {/* Delete Button - More Prominent */}
        <button
          onClick={handleDelete}
          disabled={isLoading}
          className={`
            p-2 rounded-lg transition-all duration-200
            text-red-500 hover:text-red-700 hover:bg-red-50
            group-hover:opacity-100 opacity-0
            ${isLoading ? "opacity-50 cursor-not-allowed" : ""}
          `}
          aria-label="Delete task"
        >
          {isLoading ? (
            <Loader2 className="w-5 h-5 animate-spin" aria-hidden="true" />
          ) : (
            <Trash2
              className="w-5 h-5 transition-transform duration-200 hover:scale-110 hover:rotate-12"
              aria-hidden="true"
            />
          )}
        </button>

        {/* Animated Action Menu */}
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
              group-hover:opacity-100 opacity-0
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
                bg-white border border-gray-200 rounded-lg shadow-xl z-20
                animate-[slideIn_0.2s_ease-out]
                overflow-hidden
              `}
              role="menu"
            >
              <button
                onClick={handleEdit}
                className="
                  w-full flex items-center gap-3 px-4 py-3 text-sm
                  text-gray-700 hover:bg-blue-50 hover:text-blue-700
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
              <div className="border-t border-gray-100" />
              <button
                onClick={handleDelete}
                disabled={isLoading}
                className="
                  w-full flex items-center gap-3 px-4 py-3 text-sm
                  text-red-600 hover:bg-red-50
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
      </div>
    </div>
  );
}
