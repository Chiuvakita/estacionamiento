import NavbarAdmin from "@/components/NavbarAdmin";

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  return (
    <div>
      <NavbarAdmin />

      <div className="p-6">
        {children}
      </div>
    </div>
  );
}
