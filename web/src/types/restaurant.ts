export interface Restaurant {
  id: string
  name: string
  district: string
  address: string
  phone: string
  longitude: number
  latitude: number
  rating: number | null
  cost: number | null
  tags: string[]
  cover: string
  source_keyword: string
  update_time: string
}
