import { SignOutButton, SignedIn } from "@clerk/nextjs";
import ProfileImage from "./profile-image";
import LinksDropdown from "./links-dropdown";

export function Navbar() {
    return (
        <SignedIn>
            <nav className="border-b bg-white flex">
                <div className="container flex flex-col items-end gap-4 py-8">
                    <LinksDropdown />
                </div>
            </nav>
        </SignedIn>
    );
}