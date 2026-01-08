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
  { value: "completed", label: "Completed" },
] as const;

interface TaskFiltersProps {
  defaultFilter?: "all" | "pending" | "completed";
  onFilterChange?: (filter: "all" | "pending" | "completed") => void;
}

export function TaskFilters({
  defaultFilter = "all",
  onFilterChange,
}: TaskFiltersProps) {
  const [activeFilter, setActiveFilter] = useState(defaultFilter);

  const handleFilterChange = (
    filter: "all" | "pending" | "completed"
  ) => {
    setActiveFilter(filter);
    onFilterChange?.(filter);
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 mb-6">
      <div className="flex gap-2" role="group" aria-label="Filter by status">
        {FILTER_OPTIONS.map((option) => (
          <button
            key={option.value}
            onClick={() => handleFilterChange(option.value)}
            className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              activeFilter === option.value
                ? "bg-blue-600 text-white"
                : "bg-gray-100 text-gray-700 hover:bg-gray-200"
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
