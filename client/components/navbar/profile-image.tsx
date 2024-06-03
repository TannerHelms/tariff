import { fetchProfileImage } from "@/utils/actions";
import React from "react";
import { UserIcon } from "../ui/icons";

async function ProfileImage(props: React.ComponentProps<"img">) {
  const profileImage = await fetchProfileImage();
  if (profileImage) {
    return (
      <img
        {...props}
        src={profileImage}
        alt="profile"
        className="size-12 rounded-full object-cover"
      />
    );
  }
  return <UserIcon className="size-12 fill-white bg-primary rounded-full" />;
}

export default ProfileImage;
