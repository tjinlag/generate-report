import config from "../utils/config"

export const getReportAssets = async () => {
  try {
    const response = await fetch(config.API_URL + '/report');
    return {
      ok: true,
      data: await response.json(),
    }
  } catch (e) {
    console.log(e)
  }

  return {
    ok: false,
    data: null,
  }
}
