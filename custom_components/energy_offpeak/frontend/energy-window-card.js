/**
 * Energy Window Tracker Lovelace card
 * Shows energy window sensors from the energy_offpeak integration.
 */

const CARD_VERSION = "1.0.0";

class EnergyWindowTrackerCard extends HTMLElement {
  static getConfigElement() {
    return null;
  }

  static getStubConfig() {
    return { entities: [] };
  }

  setConfig(config) {
    this._config = config || {};
    if (this._hass) this._update();
  }

  set hass(hass) {
    this._hass = hass;
    this._update();
  }

  async _checkVersion() {
    if (this._versionCheckDone || !this._hass) return;
    this._versionCheckDone = true;
    try {
      const result = await this._hass.connection.sendMessagePromise({
        type: "energy_offpeak/version",
      });
      const backend = (result && result.version) || "0";
      if (backend !== CARD_VERSION) {
        this.dispatchEvent(
          new CustomEvent("hass-notification", {
            detail: {
              message: `Energy Window Tracker: version mismatch (backend ${backend}, card ${CARD_VERSION}). Reload the dashboard.`,
              duration: 5000,
              dismissable: true,
            },
            bubbles: true,
            composed: true,
          })
        );
      }
    } catch (_) {
      this._versionCheckDone = false;
    }
  }

  getCardSize() {
    const entities = (this._config && this._config.entities) || [];
    return Math.max(1, Math.min(entities.length + 1, 8));
  }

  _update() {
    if (!this._hass || !this._config) return;
    this._checkVersion();
    const entities = this._config.entities || [];
    const showEmpty = entities.length === 0;
    const states = showEmpty
      ? []
      : entities
          .map((e) => {
            const id = typeof e === "string" ? e : e.entity;
            const state = id ? this._hass.states[id] : null;
            return state ? { id, name: state.attributes.friendly_name || id, state: state.state, unit: state.attributes.unit_of_measurement } : null;
          })
          .filter(Boolean);

    if (!this.shadowRoot) {
      this.attachShadow({ mode: "open" });
    }
    const card = document.createElement("ha-card");
    card.header = "Energy Window Tracker";
    const content = document.createElement("div");
    content.style.padding = "16px";

    if (showEmpty) {
      content.innerHTML = "<p>Add Energy Window entities to this card from the card configuration.</p>";
    } else {
      const list = document.createElement("div");
      list.style.display = "flex";
      list.style.flexDirection = "column";
      list.style.gap = "8px";
      states.forEach(({ name, state, unit }) => {
        const row = document.createElement("div");
        row.style.display = "flex";
        row.style.justifyContent = "space-between";
        row.style.alignItems = "center";
        const nameEl = document.createElement("span");
        nameEl.textContent = name || "—";
        const valueEl = document.createElement("span");
        valueEl.textContent = `${state} ${unit || ""}`.trim();
        valueEl.style.fontWeight = "500";
        row.appendChild(nameEl);
        row.appendChild(valueEl);
        list.appendChild(row);
      });
      content.appendChild(list);
    }
    card.appendChild(content);
    this.shadowRoot.innerHTML = "";
    this.shadowRoot.appendChild(card);
  }
}

customElements.define("energy-window-tracker-card", EnergyWindowTrackerCard);

window.customCards = window.customCards || [];
window.customCards.push({
  type: "energy-window-tracker-card",
  name: "Energy Window Tracker",
  description: "Display energy use during your configured time windows",
  preview: true,
});
