declare global {
  interface Window { AMap: any }
}

const AMAP_KEY = '9947469adb0fcc44af702e74f5aa536f'
const AMAP_VERSION = '2.0'

let loadPromise: Promise<any> | null = null

export function loadAMap(): Promise<any> {
  if (loadPromise) return loadPromise
  if (typeof window.AMap !== 'undefined') {
    return Promise.resolve(window.AMap)
  }
  loadPromise = new Promise((resolve, reject) => {
    const script = document.createElement('script')
    script.src = `https://webapi.amap.com/maps?v=${AMAP_VERSION}&key=${AMAP_KEY}`
    script.async = true
    script.onload = () => {
      if (typeof window.AMap !== 'undefined') {
        resolve(window.AMap)
      } else {
        reject(new Error('高德地图API加载失败'))
      }
    }
    script.onerror = () => reject(new Error('高德地图API加载失败，请检查网络'))
    document.head.appendChild(script)
  })
  return loadPromise
}
