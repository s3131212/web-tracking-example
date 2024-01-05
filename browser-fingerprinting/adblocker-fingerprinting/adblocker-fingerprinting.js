const filters = {
    easyList: '#Ads_google_bottom_wide',
    easyListChina: '#xinnxi',
    easyListCookie: '#CookieEnableBox',
    easyListGermany: '#WerbungObenRechts8_GesamtDIV',
    easylistPortuguese: '#pubCofinaFotogaleria',
    easyListSpanish: '#publicidad_lateral_medio',
}


function getActiveFilterLists() {
    const filterNames = Object.keys(filters)
    const allSelectors = Object.values(filters)
    const blockedSelectors = getBlockedSelectors(allSelectors)

    const activeFilterLists = filterNames.filter(name => blockedSelectors.has(filters[name]))

    return activeFilterLists
}

function getBlockedSelectors(selectors) {
    const root = document.createElement('div')
    const elements = []
    const blockedSelectors = new Set()

    overrideDisplay(root)

    for (let i = 0; i < selectors.length; ++i) {
        const element = createElementFromSelector(selectors[i])
        overrideDisplay(element)
        root.appendChild(element)
        elements.push(element)
    }

    document.body.appendChild(root)

    try {
        for (let i = 0; i < selectors.length; ++i) {
            if (!elements[i].offsetParent) {
                blockedSelectors.add(selectors[i])
            }
        }
    } catch (e) {
        console.error(e)
    } finally {
        document.body.removeChild(root)
    }

    return blockedSelectors
}

function overrideDisplay(element) {
    element.style.setProperty('display', 'block', 'important')
}

function createElementFromSelector(selector) {
    if (selector.startsWith('#')) {
        const div = document.createElement('div')
        div.id = selector.slice(1)
        return div
    }
    if (selector.startsWith('.')) {
        const div = document.createElement('div')
        div.className = selector.slice(1)
        return div
    }
    return null;
}