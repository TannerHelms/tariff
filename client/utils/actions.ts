'use server'

import { Job, Status } from "@prisma/client"
import db from "./db"
import productQueue from "./redis"
import { Product } from "./types"
import { currentUser } from "@clerk/nextjs/server"

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
    return db.job.findMany()
}

export const restartJob = async (jobId: string) => {
    const job = await db.job.update({
        where: {
            id: jobId
        },
        data: {
            status: Status.PENDING,
            result: null,
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


export const deleteJob = async (jobId: string) => {
    return db.job.delete({
        where: {
            id: jobId
        }
    })
}

export const fetchProfileImage = async () => {
    const user = await currentUser();
    if (!user) return null;
    return user.imageUrl;;
}