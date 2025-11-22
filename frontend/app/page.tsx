export default async function Home() {
    const res = await fetch("http://localhost:8000", { cache: "no-store" });
    const data = await res.json();

    return (
        <div style={{ padding: 20 }}>
            <h1>Frontend → Backend Test</h1>
            <p>{data.message}</p>
        </div>
    );
}
