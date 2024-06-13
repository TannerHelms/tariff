import React from "react";
export type IconComponent = (
    props: React.ComponentPropsWithoutRef<"svg">
) => JSX.Element;

export const TentIcon: IconComponent = (props) => {
    return (
        <svg {...props} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
            <title>Home</title>
            <g id="1716490868431-7575068_SVGRepo_iconCarrier">
                <path
                    className="st0"
                    d="M463.534,418.371L271.805,117.509l23.66-37.108l-22.497-14.328L256,92.703l-16.966-26.629l-22.498,14.328 l23.644,37.108L48.466,418.371H0v27.556h512v-27.556H463.534z M287.94,418.371l-19.199-95.998l66.769,95.998H287.94z M354.85,418.371l-99.635-138.542l-1.21-5.452L188.21,418.371H80.091L256,142.323l175.909,276.047H354.85z"
                ></path>
            </g>
        </svg>
    );
};
export const AddIcon: IconComponent = (props) => {
    return (
        <svg {...props} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <circle cx="12" cy="12" r="10" stroke="#1C274C" stroke-width="1.5"></circle> <path d="M15 12L12 12M12 12L9 12M12 12L12 9M12 12L12 15" stroke="#1C274C" stroke-width="1.5" stroke-linecap="round"></path> </g></svg>
    );
};

export const UserIcon: IconComponent = (props) => {
    return (
        <svg {...props} viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
            <path
                className="st0"
                d="M341.942,356.432c-20.705-12.637-28.134-11.364-28.134-36.612c0-8.837,0-25.256,0-40.403 c11.364-12.62,15.497-11.049,25.107-60.597c19.433,0,18.174-25.248,27.34-47.644c7.471-18.238,1.213-25.632-5.08-28.654 c5.144-66.462,5.144-112.236-70.292-126.436c-27.344-23.437-68.605-15.48-88.158-11.569c-19.536,3.911-37.159,0-37.159,0 l3.356,31.49c-28.608,34.332-14.302,80.106-18.908,106.916c-6.002,3.27-11.416,10.809-4.269,28.253 c9.165,22.396,7.906,47.644,27.34,47.644c9.61,49.548,13.742,47.977,25.107,60.597c0,15.147,0,31.566,0,40.403 c0,25.248-8.581,25.683-28.133,36.612c-47.14,26.349-108.569,41.658-119.575,124.01C48.468,495.504,134.952,511.948,256,512 c121.048-0.052,207.528-16.496,205.517-31.558C450.511,398.09,388.519,384.847,341.942,356.432z"
            />
        </svg>
    );
};

export const AlignLeftIcon: IconComponent = (props) => {
    return (
        <svg
            {...props}
            height="24"
            width="24"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
        >
            <g
                fill="none"
                stroke="#212121"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
            >
                <path d="M21 6L3 6" />
                <path d="M15 12L3 12" />
                <path d="M17 18L3 18" />
            </g>
        </svg>
    );
};