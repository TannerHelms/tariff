"use client";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { getJobs } from "@/utils/actions";
import { Job } from "@prisma/client";
import { ReloadIcon } from "@radix-ui/react-icons";
import { useEffect, useState } from "react";
import { Card } from "../ui/card";
import { ScrollArea } from "../ui/scroll-area";
import { Separator } from "../ui/separator";

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

      <Card className="rounded-xl p-4 w-[400px] bg-white">
        <h3 className="my-4">Products</h3>
        <Separator className=" my-4" />
        <ScrollArea className="h-[500px]">
          <ul className="space-y-4">
            {!jobs && <ReloadIcon className="h-4 w-4 animate-spin mx-auto" />}
            {jobs && jobs.length === 0 && (
              <p className="text-center">No jobs found</p>
            )}
            {jobs &&
              jobs.length > 0 &&
              jobs.map((job) => {
                const payload = JSON.parse(job.payload);
                return (
                  <li key={job.id}>
                    <Card className="p-2 flex flex-row justify-between lowercase items-center">
                      <p
                        className="cursor-pointer hover:underline"
                        onClick={() => {
                          setJob({ ...job, payload: JSON.parse(job.payload) });
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
                        <p className="text-green-400">completed</p>
                      )}
                    </Card>
                  </li>
                );
              })}
          </ul>
        </ScrollArea>
      </Card>
    </>
  );
}
