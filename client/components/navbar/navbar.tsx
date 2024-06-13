import LinksDropdown from "./links-dropdown";

export function Navbar() {
    return (
        <nav className="border-b bg-white flex">
            <div className="container flex flex-col items-end gap-4 py-8">
                <LinksDropdown />
            </div>
        </nav>
    );
}