/**
 * TaskFilters component.
 *
 * Provides filtering options for tasks (all, pending, completed).
 */

"use client";

import { useState } from "react";

const FILTER_OPTIONS = [
  { value: "all", label: "All Tasks" },
  { value: "pending", label: "Pending" },
  { value: "in_progress", label: "In Progress" },
  { value: "completed", label: "Completed" },
] as const;

interface TaskFiltersProps {
  defaultFilter?: "all" | "pending" | "in_progress" | "completed";
  onFilterChange?: (filter: "all" | "pending" | "in_progress" | "completed") => void;
}

export function TaskFilters({
  defaultFilter = "all",
  onFilterChange,
}: TaskFiltersProps) {
  const [activeFilter, setActiveFilter] = useState(defaultFilter);

  const handleFilterChange = (
    filter: "all" | "pending" | "in_progress" | "completed"
  ) => {
    setActiveFilter(filter);
    onFilterChange?.(filter);
  };

  return (
    <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4 mb-6">
      <div className="flex gap-2" role="group" aria-label="Filter by status">
        {FILTER_OPTIONS.map((option) => (
          <button
            key={option.value}
            onClick={() => handleFilterChange(option.value)}
            className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              activeFilter === option.value
                ? "bg-blue-600 dark:bg-blue-500 text-white"
                : "bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600"
            }`}
            aria-pressed={activeFilter === option.value}
          >
            {option.label}
          </button>
        ))}
      </div>
    </div>
  );
}
