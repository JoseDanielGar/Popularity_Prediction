export async function callApi(values) {
  try {
    const response = await fetch(`api/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(values)
    })
    if (!response.ok) throw new Error("API error")
    return await response.json()
  } catch (err) {
    console.error(err)
    return null
  }
}