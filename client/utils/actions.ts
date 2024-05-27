'use server'

import { Job, Status } from "@prisma/client"
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
            updatedAt: "desc"
        }
    })
}

export const restartJob = async (jobId: string) => {
    const job = await db.job.update({
        where: {
            id: jobId
        },
        data: {
            status: Status.PENDING
        }
    })

    if (!job) {
        throw new Error("Job not found")
    }

    const payload = JSON.parse(job.payload)

    await productQueue.add("product", {
        jobId: job.id,
        ...payload
    })
}