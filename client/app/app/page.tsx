"use client";
import ProductForm from "@/components/product/product-form";
import ProductList from "@/components/product/product-list";

export default function Home() {
  return (
    <main className="flex justify-center mt-40">
      <ProductList />
    </main>
  );
}
