import type { APIRoute } from "astro";
import { Resend } from "resend";
// 1. Ubah import sesuai nama file dan komponen baru lo
import { Commission } from "../../../emails/CommissionTemplate";

const resend = new Resend(import.meta.env.RESEND_API_KEY);

export const POST: APIRoute = async ({ request }) => {
  try {
    const body = await request.json();
    const { name, contact, category, packageName, description } = body;

    const { data, error } = await resend.emails.send({
      from: "Commission Form <onboarding@resend.dev>",
      to: ["hikamalrosyid@gmail.com"], 
      subject: `🎨 Commission Order: ${name} [${category}]`,
      // 2. Panggil komponen 'Commission' bukan 'ContactUsEmail'
      react: Commission({ 
        senderName: name, 
        senderEmail: contact, 
        category: category,
        packageName: packageName,
        description: description 
      }),
    });

    if (error) {
      return new Response(JSON.stringify({ error }), { status: 400 });
    }

    return new Response(JSON.stringify(data), { status: 200 });
  } catch (e) {
    return new Response(JSON.stringify({ message: "Internal Server Error" }), { status: 500 });
  }
};