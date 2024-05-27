'use server'

import { Job } from "@prisma/client"
import db from "./db"
import productQueue from "./redis"
import { Product } from "./types"

export const createProduct = async (product: Product) => {

    const job = await db.job.create({
        data: {
            type: "product",
            payload: JSON.stringify(product),
        }
    })

    await productQueue.add("product", {
        jobId: job.id,
        ...product
    })
}

export const getJobs = async (): Promise<Job[]> => {
    return db.job.findMany({
        orderBy: {
            createdAt: "desc"
        }
    })
}