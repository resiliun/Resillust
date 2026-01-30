import type { APIRoute } from "astro";
import { Resend } from "resend";
// Import template email kamu (pastikan path-nya benar)
import { ContactUsEmail } from "../../../emails/sampleemail";

const resend = new Resend(import.meta.env.RESEND_API_KEY);

export const POST: APIRoute = async ({ request }) => {
  try {
    // Ambil data dari form frontend
    const body = await request.json();
    const { name, email, message } = body;

    // Kirim email menggunakan template React
    const { data, error } = await resend.emails.send({
      from: "Contact Form <onboarding@resend.dev>",
      to: ["hikamalrosyid@gmail.com"],
      subject: `Pesan Baru dari ${name}`,
      // Ganti 'html' menjadi 'react'
      react: ContactUsEmail({ 
        senderName: name, 
        senderEmail: email, 
        message: message 
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