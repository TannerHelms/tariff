"use client";
import ProductForm from "@/components/product/product-form";

export default function Home() {
    return (
        <main className="flex justify-center pt-40">
            <div className="max-w-[900px]">
                <ProductForm />
            </div>
        </main>
    );
}
