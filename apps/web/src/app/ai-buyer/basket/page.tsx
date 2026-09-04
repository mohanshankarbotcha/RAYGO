import { redirect } from "next/navigation";

export default function BasketRedirect() {
  // Basket state lives inline in /ai-buyer per PRD section 8 note
  // ("optional if not integrated in AI Buyer screen"). Kept as a route alias.
  redirect("/ai-buyer");
}
