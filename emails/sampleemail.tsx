import {
  Body,
  Button,
  Container,
  Head,
  Html,
  Hr,
  Img,
  Preview,
  Section,
  Text,
} from "@react-email/components";
import * as React from "react";

interface ContactUsEmailProps {
  senderName: string;
  senderEmail: string;
  message: string;
}

const baseUrl = "https://demo.react.email/";

export const ContactUsEmail = ({
  senderName,
  senderEmail,
  message,
}: ContactUsEmailProps) => (
  <Html>
    <Head />
    <Preview>Pesan baru dari {senderName} via Form Kontak</Preview>
    <Body style={main}>
      <Container style={container}>
        <Img
          src={`${baseUrl}/static/github.png`} // Ganti dengan logo brand kamu
          width="32"
          height="32"
          alt="Logo"
        />
        <Text style={title}>
          Pesan Baru Masuk 📨
        </Text>

        <Section style={section}>
          <Text style={text}>
            Ada pesan baru dari fitur <strong>Contact Us</strong> di website Anda:
          </Text>
          
          <Hr style={hr} />
          
          <Text style={details}>
            <strong>Nama:</strong> {senderName}
          </Text>
          <Text style={details}>
            <strong>Email:</strong> {senderEmail}
          </Text>
          <Text style={details}>
            <strong>Pesan:</strong>
          </Text>
          <Text style={messageBox}>
            {message}
          </Text>

          <Button style={button} href={`mailto:${senderEmail}`}>
            Balas Email Langsung
          </Button>
        </Section>

        <Text style={footer}>
          Email ini dikirim otomatis oleh sistem website Anda.
        </Text>
      </Container>
    </Body>
  </Html>
);

// Contoh data untuk preview saat development
ContactUsEmail.PreviewProps = {
  senderName: "Budi Utomo",
  senderEmail: "budi@example.com",
  message: "Halo, saya tertarik dengan layanan Anda. Bisakah kita berdiskusi lebih lanjut mengenai harganya?",
} as ContactUsEmailProps;

export default ContactUsEmail;

// --- STYLING ---

const main = {
  backgroundColor: "#f6f9fc",
  fontFamily: '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Oxygen-Sans,Ubuntu,Cantarell,"Helvetica Neue",sans-serif',
};

const container = {
  margin: "0 auto",
  padding: "20px 0 48px",
  maxWidth: "580px",
};

const title = {
  fontSize: "24px",
  lineHeight: "1.3",
  fontWeight: "700",
  color: "#484848",
};

const section = {
  padding: "24px",
  border: "solid 1px #dedede",
  borderRadius: "5px",
  backgroundColor: "#ffffff",
};

const text = {
  fontSize: "16px",
  lineHeight: "24px",
  textAlign: "left" as const,
};

const details = {
  fontSize: "14px",
  lineHeight: "20px",
  margin: "10px 0",
  color: "#525f7f",
};

const messageBox = {
  padding: "12px",
  backgroundColor: "#f4f4f4",
  borderRadius: "4px",
  border: "1px solid #eee",
  fontStyle: "italic",
};

const hr = {
  borderColor: "#cccccc",
  margin: "20px 0",
};

const button = {
  backgroundColor: "#5f51e8",
  borderRadius: "3px",
  color: "#fff",
  fontSize: "16px",
  textDecoration: "none",
  textAlign: "center" as const,
  display: "block",
  padding: "12px",
  marginTop: "20px",
};

const footer = {
  color: "#8898aa",
  fontSize: "12px",
  textAlign: "center" as const,
  marginTop: "30px",
};