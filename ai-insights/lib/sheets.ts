import { GoogleSpreadsheet } from "google-spreadsheet";
import { JWT } from "google-auth-library";

function formatDate(date: string) {
    if (!date) return "";

    if (date.includes(",")) {
        return date;
    }

    try {
        const d = new Date(date);

        return d.toLocaleDateString("en-GB", {
            day: "numeric",
            month: "long",
            year: "numeric",
        });
    } catch {
        return date;
    }
}

function parseRelatedSources(raw: string) {
    if (!raw) return [];
    try {
        const parsed = JSON.parse(raw);
        if (Array.isArray(parsed)) return parsed;
        return [];
    } catch {
        return [];
    }
}

export async function getInsights() {

    const auth = new JWT({
        email: process.env.GOOGLE_SERVICE_ACCOUNT_EMAIL,
        key: process.env.GOOGLE_PRIVATE_KEY?.replace(/\\n/g, "\n"),
        scopes: [
            "https://www.googleapis.com/auth/spreadsheets",
        ],
    });

    const doc = new GoogleSpreadsheet(
        process.env.GOOGLE_SHEET_ID!,
        auth
    );

    await doc.loadInfo();

    const sheet = doc.sheetsByIndex[0];

    const rows = await sheet.getRows();

    const latestRows = [...rows].reverse();

    return latestRows.map((row, index) => ({
        id: index + 1,
        date: formatDate(row.get("Date")),
        category: row.get("Category"),
        title: row.get("Title"),
        subtitle: row.get("Subtitle") || "",
        content: row.get("Blog Content"),
        imageUrl: row.get("Image URL"),
        sourceUrl: row.get("Source URL"),
        relatedSources: parseRelatedSources(row.get("Related Sources")),
    }));
}