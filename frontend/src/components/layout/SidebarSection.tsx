import React from "react";

interface Props {
  title: string;
  children: React.ReactNode;
}

const SidebarSection: React.FC<Props> = ({ title, children }) => {
  return (
    <div className="sidebar-section">
      <div className="sidebar-section-title">{title}</div>
      <div>{children}</div>
    </div>
  );
};

export default SidebarSection;
