import NavbarCliente from "@/components/NavbarCliente";

export default function ClienteLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div>
      <NavbarCliente />

      <div className="p-6">
        {children}
      </div>
    </div>
  );
}
