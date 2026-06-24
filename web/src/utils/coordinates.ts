/**
 * 深圳地图边界（与底图截图对应）
 *
 * ⚠️ 如果你截的高德地图画面范围不同，请修改这四个值。
 * 校准方法：
 *   1. 打开你的截图，找两个地标（例如：左上角的某个点和右下角的某个点）
 *   2. 在高德地图上查这两个点的经纬度
 *   3. 把 minLng=maxLng=minLat=maxLat 替换为你截图的真实边界
 */
export const SHENZHEN_BBOX = {
  minLng: 113.73,   // 深圳西侧（宝安机场以西）
  maxLng: 114.49,   // 深圳东侧（大鹏半岛）
  minLat: 22.49,    // 深圳南侧（蛇口）
  maxLat: 22.83     // 深圳北侧（光明/观澜）
}

export const MAP_IMAGE_WIDTH = 1838
export const MAP_IMAGE_HEIGHT = 946

export function lngLatToPixel(lng: number, lat: number) {
  const { minLng, maxLng, minLat, maxLat } = SHENZHEN_BBOX
  return {
    x: ((lng - minLng) / (maxLng - minLng)) * MAP_IMAGE_WIDTH,
    y: ((maxLat - lat) / (maxLat - minLat)) * MAP_IMAGE_HEIGHT
  }
}
