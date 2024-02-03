import { THEME_ENUM } from 'constants/theme.constant'

/**
 * Since some configurations need to be match with specific themes, 
 * we recommend to use the configuration that generated from demo.
 */

export const themeConfig = {
    themeColor: 'purple',
    direction: THEME_ENUM.DIR_LTR,
    mode: THEME_ENUM.NAV_MODE_DARK,
    locale: 'en',
    primaryColorLevel: 400,
    cardBordered: true,
    panelExpand: false,
    controlSize: 'md',
    navMode: THEME_ENUM.NAV_MODE_THEMED,
    layout: {
        type: THEME_ENUM.LAYOUT_TYPE_DECKED,
        sideNavCollapse: false,
    },
}
