var objectFitImages = function () {
    "use strict";
    var i = "bfred-it:object-fit-images", o = /(object-fit|object-position)\s*:\s*([-.\w\s%]+)/g,
        t = "undefined" == typeof Image ? {style: {"object-position": 1}} : new Image, n = "object-fit" in t.style,
        c = "object-position" in t.style, s = "background-size" in t.style, a = "string" == typeof t.currentSrc,
        u = t.getAttribute, l = t.setAttribute, g = !1;

    function f(t, e, r) {
        var n = function (t, e) {
            return "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='" + t + "' height='" + e + "'%3E%3C/svg%3E"
        }(e || 1, r || 0);
        u.call(t, "src") !== n && l.call(t, "src", n)
    }

    function d(t, e) {
        t.naturalWidth ? e(t) : setTimeout(d, 100, t, e)
    }

    function b(e) {
        var t = function (t) {
            for (var e, r = getComputedStyle(t).fontFamily, n = {}; null !== (e = o.exec(r));) n[e[1]] = e[2];
            return n
        }(e), r = e[i];
        if (t["object-fit"] = t["object-fit"] || "fill", !r.img) {
            if ("fill" === t["object-fit"]) return;
            if (!r.skipTest && n && !t["object-position"]) return
        }
        if (!r.img) {
            r.img = new Image(e.width, e.height), r.img.srcset = u.call(e, "data-ofi-srcset") || e.srcset, r.img.src = u.call(e, "data-ofi-src") || e.src, l.call(e, "data-ofi-src", e.src), e.srcset && l.call(e, "data-ofi-srcset", e.srcset), f(e, e.naturalWidth || e.width, e.naturalHeight || e.height), e.srcset && (e.srcset = "");
            try {
                !function (r) {
                    var e = {
                        get: function (t) {
                            return r[i].img[t || "src"]
                        }, set: function (t, e) {
                            return r[i].img[e || "src"] = t, l.call(r, "data-ofi-" + e, t), b(r), t
                        }
                    };
                    Object.defineProperty(r, "src", e), Object.defineProperty(r, "currentSrc", {
                        get: function () {
                            return e.get("currentSrc")
                        }
                    }), Object.defineProperty(r, "srcset", {
                        get: function () {
                            return e.get("srcset")
                        }, set: function (t) {
                            return e.set(t, "srcset")
                        }
                    })
                }(e)
            } catch (t) {
                window.console && console.warn("https://bit.ly/ofi-old-browser")
            }
        }
        !function (t) {
            if (t.srcset && !a && window.picturefill) {
                var e = window.picturefill._;
                t[e.ns] && t[e.ns].evaled || e.fillImg(t, {reselect: !0}), t[e.ns].curSrc || (t[e.ns].supported = !1, e.fillImg(t, {reselect: !0})), t.currentSrc = t[e.ns].curSrc || t.src
            }
        }(r.img), e.style.backgroundImage = 'url("' + (r.img.currentSrc || r.img.src).replace(/"/g, '\\"') + '")', e.style.backgroundPosition = t["object-position"] || "center", e.style.backgroundRepeat = "no-repeat", e.style.backgroundOrigin = "content-box", /scale-down/.test(t["object-fit"]) ? d(r.img, function () {
            r.img.naturalWidth > e.width || r.img.naturalHeight > e.height ? e.style.backgroundSize = "contain" : e.style.backgroundSize = "auto"
        }) : e.style.backgroundSize = t["object-fit"].replace("none", "auto").replace("fill", "100% 100%"), d(r.img, function (t) {
            f(e, t.naturalWidth, t.naturalHeight)
        })
    }

    function m(t, e) {
        var r = !g && !t;
        if (e = e || {}, t = t || "img", c && !e.skipTest || !s) return !1;
        "img" === t ? t = document.getElementsByTagName("img") : "string" == typeof t ? t = document.querySelectorAll(t) : "length" in t || (t = [t]);
        for (var n = 0; n < t.length; n++) t[n][i] = t[n][i] || {skipTest: e.skipTest}, b(t[n]);
        r && (document.body.addEventListener("load", function (t) {
            "IMG" === t.target.tagName && m(t.target, {skipTest: e.skipTest})
        }, !0), g = !0, t = "img"), e.watchMQ && window.addEventListener("resize", m.bind(null, t, {skipTest: e.skipTest}))
    }

    function r(t, e) {
        return t[i] && t[i].img && ("src" === e || "srcset" === e) ? t[i].img : t
    }

    return m.supportsObjectFit = n, (m.supportsObjectPosition = c) || (HTMLImageElement.prototype.getAttribute = function (t) {
        return u.call(r(this, t), t)
    }, HTMLImageElement.prototype.setAttribute = function (t, e) {
        return l.call(r(this, t), t, String(e))
    }), m
}();
String.prototype.padStart || (String.prototype.padStart = function (t, e) {
    return t >>= 0, e = String(void 0 !== e ? e : " "), this.length > t ? String(this) : ((t -= this.length) > e.length && (e += e.repeat(t / e.length)), e.slice(0, t) + String(this))
}), Object.assign || Object.defineProperty(Object, "assign", {
    enumerable: !1,
    configurable: !0,
    writable: !0,
    value: function (t) {
        "use strict";
        if (null == t) throw new TypeError("Cannot convert first argument to object");
        for (var e = Object(t), r = 1; r < arguments.length; r++) {
            var n = arguments[r];
            if (null != n) {
                n = Object(n);
                for (var i = Object.keys(Object(n)), o = 0, c = i.length; o < c; o++) {
                    var s = i[o], a = Object.getOwnPropertyDescriptor(n, s);
                    void 0 !== a && a.enumerable && (e[s] = n[s])
                }
            }
        }
        return e
    }
}), Array.from || (Array.from = function () {
    function l(t) {
        return "function" == typeof t || "[object Function]" === e.call(t)
    }

    function g(t) {
        var e = function (t) {
            var e = Number(t);
            return isNaN(e) ? 0 : 0 !== e && isFinite(e) ? (0 < e ? 1 : -1) * Math.floor(Math.abs(e)) : e
        }(t);
        return Math.min(Math.max(e, 0), r)
    }

    var e = Object.prototype.toString, r = Math.pow(2, 53) - 1;
    return function (t, e, r) {
        var n = Object(t);
        if (null == t) throw new TypeError("Array.from requires an array-like object - not null or undefined");
        var i, o = 1 < arguments.length ? e : void 0;
        if (void 0 !== o) {
            if (!l(o)) throw new TypeError("Array.from: when provided, the second argument must be a function");
            2 < arguments.length && (i = r)
        }
        for (var c, s = g(n.length), a = l(this) ? Object(new this(s)) : new Array(s), u = 0; u < s;) c = n[u], a[u] = o ? void 0 === i ? o(c, u) : o.call(i, c, u) : c, u += 1;
        return a.length = s, a
    }
}()), document.addEventListener("DOMContentLoaded", function () {
    objectFitImages()
});
