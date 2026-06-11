import { GoogleSpreadsheet } from "google-spreadsheet";
import { JWT } from "google-auth-library";

export async function getInsights() {
    const serviceAccountAuth = new JWT({
        email: process.env.GOOGLE_SERVICE_ACCOUNT_EMAIL,
        key: process.env.GOOGLE_PRIVATE_KEY?.replace(/\\n/g, "\n"),
        scopes: [
            "https://www.googleapis.com/auth/spreadsheets",
        ],
    });

    const doc = new GoogleSpreadsheet(
        process.env.GOOGLE_SHEET_ID!,
        serviceAccountAuth
    );

    await doc.loadInfo();

    const sheet = doc.sheetsByIndex[0];

    const rows = await sheet.getRows();

    return rows.map((row) => ({
        date: row.get("Date"),
        category: row.get("Category"),
        title: row.get("Title"),
        content: row.get("Blog Content"),
        imagePrompt: row.get("Image_prompt"),
        sourceUrl: row.get("Source URL"),
        imageUrl: row.get("Image URL"),
    }));
}