"use client";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { createProduct } from "@/utils/actions";
import { Product } from "@/utils/types";
import { ReloadIcon } from "@radix-ui/react-icons";
import { FieldValues, useForm } from "react-hook-form";
import { formValues } from "./product-form-values";

export default function ProductForm() {
  const form = useForm({
    defaultValues: {
      product: "",
      description: "",
      material: "",
      use: "",
      type: "",
    },
  });

  const handleFormSubmit = (data: FieldValues) => {
    const product: Product = {
      name: data.product,
      description: data.description,
      material: data.material,
      use: data.use,
      type: data.type,
    };
    createProduct(product);
  };

  return (
    <Card className="rounded-xl p-4 w-[400px] bg-white">
      <Form {...form}>
        <form
          onSubmit={form.handleSubmit(handleFormSubmit)}
          className="space-y-8"
        >
          {formValues.map((value) => (
            <FormField
              key={value.name}
              control={form.control}
              name={value.name}
              render={({ field }) => (
                <FormItem>
                  <FormLabel>{value.label}</FormLabel>
                  <FormControl>
                    <Input
                      placeholder={value.placeholder}
                      {...field}
                      required
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          ))}
          <Button
            className="w-full"
            type="submit"
            disabled={form.formState.isSubmitting}
          >
            {form.formState.isSubmitting ? (
              <>
                <ReloadIcon className="mr-2 h-4 w-4 animate-spin" />
                Please wait
              </>
            ) : (
              "Submit"
            )}
          </Button>
        </form>
      </Form>
    </Card>
  );
}
