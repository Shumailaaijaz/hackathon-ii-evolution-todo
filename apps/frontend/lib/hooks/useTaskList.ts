/**
 * React hook for fetching and managing task list.
 *
 * Uses SWR for data fetching with caching and revalidation.
 */

"use client";

import useSWR from "swr";
import { getTasks } from "../api";
import type { Task, TaskListParams, ApiResponse } from "../types";

interface UseTaskListParams extends TaskListParams {
  userId: string;
}

interface UseTaskListReturn {
  tasks: Task[] | undefined;
  isLoading: boolean;
  error: Error | undefined;
  mutate: () => void;
}

/**
 * Hook for fetching task list with filtering and pagination.
 *
 * @param params - Filter parameters (userId, completed, sort, order)
 * @returns Task list data, loading state, error, and mutate function
 */
export function useTaskList(params: UseTaskListParams): UseTaskListReturn {
  const { userId, ...queryParams } = params;

  const fetcher = async (): Promise<Task[]> => {
    const response = await getTasks(userId, queryParams);

    if (!response.success || !response.data) {
      throw new Error(response.error?.message || "Failed to fetch tasks");
    }

    return response.data;
  };

  const { data, error, isLoading, mutate } = useSWR<Task[]>(
    userId ? [`/api/${userId}/tasks`, JSON.stringify(queryParams)] : null,
    fetcher,
    {
      revalidateOnFocus: true,
      revalidateOnReconnect: true,
      dedupingInterval: 2000,
    }
  );

  return {
    tasks: data,
    isLoading,
    error,
    mutate,
  };
}
