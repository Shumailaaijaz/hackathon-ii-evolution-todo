/**
 * TaskCard component.
 *
 * Displays an individual task with completion toggle and action menu.
 */

"use client";

import { useState } from "react";
import {
  CheckCircle,
  Circle,
  Trash2,
  Edit2,
  MoreVertical,
  Clock,
} from "lucide-react";
import { toggleTask, deleteTask } from "@/lib/api";
import { formatRelativeTime } from "@/lib/utils/date";
import { toast } from "@/lib/utils/toast";
import type { Task } from "@/lib/types";

interface TaskCardProps {
  task: Task;
  onUpdate?: () => void;
  onDelete?: () => void;
}

export function TaskCard({ task, onUpdate, onDelete }: TaskCardProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [showMenu, setShowMenu] = useState(false);

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

    setIsLoading(true);
    try {
      await deleteTask(task.userId, task.id);
      onDelete?.();
      toast.success("Task deleted successfully");
    } catch (error) {
      console.error("Failed to delete task:", error);
      toast.error("Failed to delete task. Please try again.");
    } finally {
      setIsLoading(false);
      setShowMenu(false);
    }
  };

  // Open edit modal (to be implemented)
  const handleEdit = () => {
    setShowMenu(false);
    // TODO: Open edit modal with task data
    toast.success("Edit feature coming soon!");
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start gap-3">
        {/* Completion Checkbox */}
        <button
          onClick={handleToggleComplete}
          disabled={isLoading}
          className="mt-0.5 text-gray-400 hover:text-blue-600 transition-colors disabled:opacity-50"
          aria-label={
            task.completed ? "Mark as incomplete" : "Mark as complete"
          }
        >
          {task.completed ? (
            <CheckCircle
              className="w-5 h-5 text-green-600"
              aria-hidden="true"
            />
          ) : (
            <Circle className="w-5 h-5" aria-hidden="true" />
          )}
        </button>

        {/* Task Content */}
        <div className="flex-1 min-w-0">
          {/* Title */}
          <h3
            className={`text-lg font-medium ${
              task.completed ? "line-through text-gray-500" : "text-gray-900"
            }`}
          >
            {task.title}
          </h3>

          {/* Description */}
          {task.description && (
            <p className="text-sm text-gray-600 mt-1 line-clamp-2">
              {task.description}
            </p>
          )}

          {/* Metadata */}
          <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
            {/* Status Badge */}
            <span
              className={`px-2 py-1 rounded-full font-medium ${
                task.completed
                  ? "bg-green-100 text-green-800"
                  : "bg-gray-100 text-gray-800"
              }`}
            >
              {task.completed ? "Completed" : "Pending"}
            </span>

            {/* Created Time */}
            <span className="flex items-center gap-1">
              <Clock className="w-3 h-3" aria-hidden="true" />
              {formatRelativeTime(task.createdAt)}
            </span>
          </div>
        </div>

        {/* Action Menu */}
        <div className="relative">
          <button
            onClick={() => setShowMenu(!showMenu)}
            className="p-1 text-gray-400 hover:text-gray-600 rounded hover:bg-gray-100 transition-colors"
            aria-label="Task actions"
            aria-expanded={showMenu}
            aria-haspopup="true"
          >
            <MoreVertical className="w-5 h-5" aria-hidden="true" />
          </button>

          {/* Dropdown Menu */}
          {showMenu && (
            <div
              className="absolute right-0 mt-2 w-48 bg-white border border-gray-200 rounded-lg shadow-lg z-10"
              role="menu"
            >
              <button
                onClick={handleEdit}
                className="w-full flex items-center gap-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-t-lg"
                role="menuitem"
              >
                <Edit2 className="w-4 h-4" aria-hidden="true" />
                Edit Task
              </button>
              <button
                onClick={handleDelete}
                disabled={isLoading}
                className="w-full flex items-center gap-2 px-4 py-2 text-sm text-red-600 hover:bg-red-50 rounded-b-lg disabled:opacity-50"
                role="menuitem"
              >
                <Trash2 className="w-4 h-4" aria-hidden="true" />
                Delete Task
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
