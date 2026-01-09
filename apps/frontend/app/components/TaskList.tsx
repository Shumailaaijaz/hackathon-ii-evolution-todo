/**
 * TaskList component.
 *
 * Displays paginated list of tasks with loading, error, and empty states.
 */

"use client";

import { useTaskList } from "@/lib/hooks/useTaskList";
import { useAuth } from "@/lib/hooks/useAuth";
import { TaskCard } from "./TaskCard";
import { Spinner } from "@/lib/components/ui/Spinner";
import { EmptyState } from "@/lib/components/ui/EmptyState";
import { AlertCircle } from "lucide-react";

import type { TaskStatus } from "@/lib/types";

interface TaskListProps {
  status?: TaskStatus;
  sort?: "created_at" | "updated_at" | "title";
  order?: "asc" | "desc";
}

export function TaskList({ status, sort, order }: TaskListProps) {
  const { user, isLoading: authLoading } = useAuth();
  const {
    tasks,
    isLoading: tasksLoading,
    error,
    mutate,
  } = useTaskList({
    userId: user?.id || "",
    status,
    sort,
    order,
  });

  const isLoading = authLoading || tasksLoading;

  // Loading State
  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-12">
        <Spinner size="lg" />
        <span className="ml-3 text-gray-600">Loading tasks...</span>
      </div>
    );
  }

  // Not authenticated
  if (!user) {
    return (
      <EmptyState
        icon="🔒"
        title="Please sign in"
        description="You need to sign in to view your tasks"
      />
    );
  }

  // Error State
  if (error) {
    return (
      <div
        className="bg-red-50 border border-red-200 rounded-lg p-6 text-red-800"
        role="alert"
        aria-live="assertive"
      >
        <div className="flex items-start gap-3">
          <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="font-semibold mb-1">Failed to load tasks</h3>
            <p className="text-sm text-red-700">
              {error.message || "An unexpected error occurred. Please try again."}
            </p>
            <button
              onClick={() => mutate()}
              className="mt-3 text-sm font-medium text-red-800 hover:text-red-900 underline"
            >
              Retry
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Empty State
  if (!tasks || tasks.length === 0) {
    const emptyMessage =
      status === "completed"
        ? {
            icon: "🎉",
            title: "No completed tasks",
            description: "Complete a task to see your progress here.",
          }
        : status === "pending"
        ? {
            icon: "✅",
            title: "No pending tasks",
            description: "All caught up! Create a new task to get started.",
          }
        : status === "in_progress"
        ? {
            icon: "⏳",
            title: "No tasks in progress",
            description: "Start working on a task to see it here.",
          }
        : {
            icon: "📝",
            title: "No tasks yet",
            description: "Create your first task to get started",
          };

    return <EmptyState {...emptyMessage} />;
  }

  // Success State
  return (
    <div className="space-y-4">
      {/* Task List */}
      <div className="space-y-3">
        {tasks.map((task) => (
          <TaskCard key={task.id} task={task} onUpdate={mutate} onDelete={mutate} />
        ))}
      </div>

      {/* Results Summary */}
      <p className="text-center text-sm text-gray-500 mt-4">
        Showing {tasks.length} task{tasks.length !== 1 ? "s" : ""}
      </p>
    </div>
  );
}
