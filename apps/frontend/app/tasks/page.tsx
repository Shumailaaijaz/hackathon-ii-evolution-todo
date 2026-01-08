/**
 * Tasks page - Main task management interface.
 *
 * Displays user's tasks with filtering and creation capabilities.
 */

"use client";

import { useState } from "react";
import { TaskList } from "../components/TaskList";
import { CreateTaskForm } from "../components/CreateTaskForm";
import { TaskFilters } from "../components/TaskFilters";

export default function TasksPage() {
  const [activeFilter, setActiveFilter] = useState<
    "all" | "pending" | "completed"
  >("all");
  const [refreshKey, setRefreshKey] = useState(0);

  const handleFilterChange = (filter: "all" | "pending" | "completed") => {
    setActiveFilter(filter);
  };

  const handleTaskCreated = () => {
    // Trigger a refresh by changing the key
    setRefreshKey((prev) => prev + 1);
  };

  // Convert filter to completed param
  const completedFilter =
    activeFilter === "pending"
      ? false
      : activeFilter === "completed"
      ? true
      : undefined;

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
          <p className="text-sm text-gray-600 mt-1">
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
        completed={completedFilter}
        sort="created_at"
        order="desc"
      />
    </div>
  );
}
