import { redirect } from "next/navigation";

export default async function RootPage() {
    // const user = await currentUser()
    // if (user) redirect("/app")
    return redirect("/login")
}