
// import { SignOutButton } from "@clerk/nextjs";
import { Button } from "../ui/button";
import { DropdownMenu, DropdownMenuContent, DropdownMenuTrigger } from "../ui/dropdown-menu";
import { AlignLeftIcon } from "../ui/icons";
import ProfileImage from "./profile-image";

const links: { name: string; href: string }[] = [
    { name: "Dashboard", href: "/app" },
    { name: "profile", href: "/app/user-profile" },
    { name: "Create", href: "/app/create" },
];

export default function LinksDropdown() {
    return (
        <DropdownMenu>
            <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="size-12 rounded-full hover:bg-white p-0">
                    <ProfileImage />
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent className="w-52" align="start" sideOffset={10} alignOffset={-52}>
                {links.map((link) => (
                    <a key={link.href} href
                        ={link.href} className="block px-4 py-2 text-gray-800 hover:bg-gray-100">{link.name}</a>
                ))}

                {/* <SignOutButton>
                    <button className="w-full block px-4 py-2 text-gray-800 hover:bg-gray-100 text-left">Sign out</button>
                </SignOutButton> */}
            </DropdownMenuContent>
        </DropdownMenu>
    )
}