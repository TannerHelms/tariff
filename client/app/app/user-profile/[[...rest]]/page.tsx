import { UserProfile } from "@clerk/nextjs";

export default function UserProfilePage() {
    return (
        <div className="w-full flex justify-center mt-20">

            <UserProfile />
        </div>
    );
}