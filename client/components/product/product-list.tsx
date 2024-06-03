"use client";
import JsonFormatter from "react-json-formatter";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { deleteJob, getJobs, restartJob } from "@/utils/actions";
import { Job, Status } from "@prisma/client";
import { ReloadIcon, TrashIcon } from "@radix-ui/react-icons";
import { useEffect, useState } from "react";
import { Card } from "../ui/card";
import { ScrollArea } from "../ui/scroll-area";
import { Separator } from "../ui/separator";
import { Product } from "@/utils/types";
import { AddIcon } from "../ui/icons";
import Link from "next/link";

export default function ProductList() {
  const [jobs, setJobs] = useState<Job[] | null>(null);
  const [modal, setModal] = useState(false);
  const [job, setJob] = useState<any>(null);

  useEffect(() => {
    const interval = setInterval(() => {
      getJobs().then((jobs) => {
        setJobs(jobs);
      });
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <>
      <Dialog open={modal} onOpenChange={setModal}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle>{job?.payload.name}</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div className="flex flex-row justify-between w-full">
              <p>Description</p>
              <p>{job?.payload.description}</p>
            </div>
            <div className="flex flex-row justify-between w-full">
              <p>Material</p>
              <p>{job?.payload.material}</p>
            </div>
            <div className="flex flex-row justify-between w-full">
              <p>Type</p>
              <p>{job?.payload.type}</p>
            </div>
            <div className="flex flex-row justify-between w-full">
              <p>Use</p>
              <p>{job?.payload.use}</p>
            </div>
            <div className="flex flex-row justify-between w-full">
              <p>Status</p>
              <p>{job?.status}</p>
            </div>
            <div className="flex flex-row justify-between w-full">
              <p>Payload</p>
              <p>{job?.result}</p>
            </div>
          </div>
        </DialogContent>
      </Dialog>

      <Card className="rounded-xl p-4 w-[400px] sm:w-[600px] lg:w-[1000px] bg-white">
        <div className="flex flex-row justify-between items-center">
          <h3 className="my-4">Products</h3>
          <Link href="/app/create">
            <AddIcon className="rounded-full size-7" />
          </Link>
        </div>
        <Separator className=" my-4" />
        <ScrollArea className="h-[500px]">
          <ul className="space-y-4">
            {!jobs && <ReloadIcon className="h-4 w-4 animate-spin mx-auto" />}
            {jobs && jobs.length === 0 && (
              <p className="text-center">No jobs found</p>
            )}
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">

              {jobs &&
                jobs.length > 0 &&
                jobs.map((job) => {
                  const payload = JSON.parse(job.payload) as Product;
                  let border = "";
                  if (job.status === Status.FAILED) {
                    border = "border-red-500 h-[400px]";
                  } else if (job.status === Status.PENDING) {
                    border = "border-blue-500 h-[400pxpx]";
                  } else if (job.status === Status.PROCESSING) {
                    border = "border-yellow-500 h-[400px]";
                  }

                  return (
                    <li key={job.id}>
                      <Card className={`${border}`}>
                        <div className="p-2 flex flex-row justify-between lowercase items-center">
                          <p
                            className="cursor-pointer hover:underline"
                            onClick={() => {
                              setJob({
                                ...job,
                                payload: JSON.parse(job.payload),
                              });
                              setModal(true);
                            }}
                          >
                            {payload.name}
                          </p>
                          {job.status === "PENDING" && (
                            <p className="text-blue-400">pending</p>
                          )}
                          {job.status === "PROCESSING" && (
                            <ReloadIcon className="mr-2 h-4 w-4 animate-spin" />
                          )}
                          {job.status === "COMPLETED" && (
                            <div className="flex flex-row gap-2 items-center">
                              <ReloadIcon
                                className="cursor-pointer size-5"
                                onClick={() => restartJob(job.id)}
                              />
                              <TrashIcon
                                className="cursor-pointer size-5"
                                onClick={() => deleteJob(job.id)}
                              />
                            </div>
                          )}
                        </div>
                        {job.result && (
                          <>
                            <Separator className="my-2" />
                            <div className="px-2">
                              <JsonFormatter json={job.result} tabWith={4} />
                            </div>
                          </>
                        )}
                      </Card>
                    </li>
                  );
                })}
            </div>
          </ul>
        </ScrollArea>
      </Card>
    </>
  );
}
