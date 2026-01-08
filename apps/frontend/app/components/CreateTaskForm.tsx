/**
 * CreateTaskForm component.
 *
 * Modal form for creating new tasks with validation.
 */

"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Modal } from "@/lib/components/ui/Modal";
import { Button } from "@/lib/components/ui/Button";
import { Input } from "@/lib/components/ui/Input";
import { Textarea } from "@/lib/components/ui/Textarea";
import { createTask } from "@/lib/api";
import { useAuth } from "@/lib/hooks/useAuth";
import { toast } from "@/lib/utils/toast";
import { Plus } from "lucide-react";

// Validation Schema
const taskSchema = z.object({
  title: z
    .string()
    .min(1, "Title is required")
    .max(200, "Title must be less than 200 characters")
    .trim(),
  description: z
    .string()
    .max(1000, "Description must be less than 1000 characters")
    .optional()
    .transform((val) => val?.trim() || undefined),
});

type TaskFormData = z.infer<typeof taskSchema>;

interface CreateTaskFormProps {
  onSuccess?: () => void;
}

export function CreateTaskForm({ onSuccess }: CreateTaskFormProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { user } = useAuth();

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<TaskFormData>({
    resolver: zodResolver(taskSchema),
    defaultValues: {
      title: "",
      description: "",
    },
  });

  const onSubmit = async (data: TaskFormData) => {
    if (!user) {
      toast.error("You must be signed in to create tasks");
      return;
    }

    setIsSubmitting(true);
    try {
      await createTask(user.id, data);
      reset();
      setIsOpen(false);
      onSuccess?.();
      toast.success("Task created successfully");
    } catch (error) {
      console.error("Failed to create task:", error);
      toast.error("Failed to create task. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleClose = () => {
    if (!isSubmitting) {
      setIsOpen(false);
      reset();
    }
  };

  return (
    <>
      {/* Trigger Button */}
      <Button
        onClick={() => setIsOpen(true)}
        variant="primary"
        size="md"
        icon={<Plus className="w-4 h-4" />}
      >
        New Task
      </Button>

      {/* Modal */}
      <Modal isOpen={isOpen} onClose={handleClose} title="Create New Task">
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          {/* Title Field */}
          <div>
            <label
              htmlFor="title"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Title <span className="text-red-600">*</span>
            </label>
            <Input
              id="title"
              {...register("title")}
              placeholder="Enter task title"
              error={errors.title?.message}
              autoFocus
              disabled={isSubmitting}
            />
          </div>

          {/* Description Field */}
          <div>
            <label
              htmlFor="description"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Description{" "}
              <span className="text-xs text-gray-500">(optional)</span>
            </label>
            <Textarea
              id="description"
              {...register("description")}
              placeholder="Enter task description"
              rows={4}
              error={errors.description?.message}
              disabled={isSubmitting}
            />
          </div>

          {/* Action Buttons */}
          <div className="flex justify-end gap-3 pt-4 border-t border-gray-200">
            <Button
              type="button"
              onClick={handleClose}
              variant="secondary"
              disabled={isSubmitting}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="primary"
              disabled={isSubmitting}
              loading={isSubmitting}
            >
              {isSubmitting ? "Creating..." : "Create Task"}
            </Button>
          </div>
        </form>
      </Modal>
    </>
  );
}
