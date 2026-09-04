import { redirect } from "next/navigation";

export default function AuditDetailRedirect() {
  // Detail is presented as a drawer on /audit; this route exists to satisfy
  // deep links from PRD section 8 (/audit/:id) and redirects into that UI.
  redirect("/audit");
}
