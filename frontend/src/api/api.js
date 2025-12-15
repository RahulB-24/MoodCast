import axios from "axios"

const client = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_URL,
  timeout: 20000,
})

export async function uploadAudio(file, onUploadProgress) {
  const form = new FormData()
  form.append("file", file)

  const res = await client.post("/predict_audio", form, {
    onUploadProgress,
  })

  return res.data
}

export async function searchByMood(payload) {
  const res = await client.post("/recommend_v3/search_by_mood", payload)
  return res.data
}

export async function searchTracks(query) {
  const res = await client.get("/search/tracks", { params: { query } })
  return res.data
}

export async function searchArtists(query) {
  const res = await client.get("/search/artists", { params: { query } })
  return res.data
}

export async function getGenres() {
  const res = await client.get("/search/genres")
  return res.data
}

export async function getAuthUrl() {
  const res = await client.get("/auth/login")
  return res.data
}

export default client
