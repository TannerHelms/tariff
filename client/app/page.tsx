"use client";
import ProductForm from "@/components/product/product-form";
import ProductList from "@/components/product/product-list";
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

export default function Home() {
  return (
    <main className="min-h-screen min-w-screen flex items-center justify-center bg-gray-200">
      <div className="grid sm:grid-cols-2 max-w-[900px] gap-2">
        <ProductForm />
        <ProductList />
      </div>
    </main>
  );
}
