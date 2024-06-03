import { SignIn } from "@clerk/nextjs";
import { currentUser } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";

export default async function RootPage() {
    const user = await currentUser()
    if (user) redirect("/app")
    return redirect("/login")
}