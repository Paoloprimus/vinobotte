import { createClient } from "@supabase/supabase-js";

let client;

// Client con chiave segreta: usato SOLO sul server, mai nel browser.
export function db() {
  if (!client) {
    client = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SECRET_KEY, {
      auth: { persistSession: false },
    });
  }
  return client;
}
