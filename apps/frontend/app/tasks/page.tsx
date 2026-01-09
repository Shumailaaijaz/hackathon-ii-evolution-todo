/**
 * Tasks page - Main task management interface.
 *
 * Displays user's tasks with filtering and creation capabilities.
 */

"use client";

import { useState } from "react";
import { Header } from "../components/Header";
import { TaskList } from "../components/TaskList";
import { CreateTaskForm } from "../components/CreateTaskForm";
import { TaskFilters } from "../components/TaskFilters";

import type { TaskStatus } from "@/lib/types";

export default function TasksPage() {
  const [activeFilter, setActiveFilter] = useState<
    "all" | "pending" | "in_progress" | "completed"
  >("all");
  const [refreshKey, setRefreshKey] = useState(0);

  const handleFilterChange = (filter: "all" | "pending" | "in_progress" | "completed") => {
    setActiveFilter(filter);
  };

  const handleTaskCreated = () => {
    // Trigger a refresh by changing the key
    setRefreshKey((prev) => prev + 1);
  };

  // Convert filter to status param
  const statusFilter: TaskStatus | undefined =
    activeFilter === "all" ? undefined : (activeFilter as TaskStatus);

  return (
    <>
      <Header />
      <div className="container mx-auto px-4 py-8 max-w-4xl">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">My Tasks</h1>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            Organize and track your work
          </p>
        </div>
        <CreateTaskForm onSuccess={handleTaskCreated} />
      </div>

      {/* Filters */}
      <TaskFilters
        defaultFilter={activeFilter}
        onFilterChange={handleFilterChange}
      />

      {/* Task List */}
      <TaskList
        key={refreshKey}
        status={statusFilter}
        sort="created_at"
        order="desc"
      />
    </div>
    </>
  );
}
