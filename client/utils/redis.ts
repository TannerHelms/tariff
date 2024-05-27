import { Queue } from 'bullmq'

const productQueue = new Queue(
    "product",
    {
        connection: {
            host: "localhost",
            port: 6379,
        },
    }
)

export default productQueue