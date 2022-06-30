![GitHub](https://img.shields.io/github/license/netsoft-ruidias/ha-custom-component-myedenred?style=for-the-badge)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

![GitHub commit activity](https://img.shields.io/github/commit-activity/m/netsoft-ruidias/ha-custom-component-myedenred?style=for-the-badge)
![GitHub Release Date](https://img.shields.io/github/release-date/netsoft-ruidias/ha-custom-component-myedenred?style=for-the-badge)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/netsoft-ruidias/ha-custom-component-myedenred?style=for-the-badge)

# myEdenred Card Integration
myEdenred - Custom Component for Home Assistant

The data source for this integration is the [MyEdenred Portugal](https://www.myedenred.pt/).

The author of this project categorically rejects any and all responsibility for the card balance and other data that were presented by the integration.

# Installation
## HACS (Recommended)
This integration can be added to HACS as a custom (non-default) repository.

Assuming you have already installed and configured HACS, follow these steps:

1. Navigate to the HACS integrations page at http://<your-home-assistant>:8123/hacs/integrations.
2. Click the 3 vertical dots menu in the top right corner.
3. Choose 'Custom repositories'
4. Enter the name of this repository (https://github.com/netsoft-ruidias/ha-custom-component-myedenred/) in the text field in the dialog.
5. Choose 'Integration' from the Category list in the dialog.
6. Click 'Add'. The repository will now be added to your HACS.
7. Click the 'x' to close the dialog.
8. The integration is now visible. Click 'Install', and click 'Install' again.
9. Ready! Now continue with the configuration.

## Manual
Manual installation is not recomended

# Configuration

## Through the interface
1. Navigate to `Settings > Devices & Services` and then click `Add Integration`
2. Search for `myEdenred`
4. Enter your credentials
5. Repeat the procedure as many times as desired to include other cards you may have

## Transactions (Display)

While showing the card's balance on a card is commonplace (any entity card will do), displaying transactions can be more complicated to achieve.

### Using a custom:html-template-card

You can use a [custom:html-template-card](https://github.com/PiotrMachowski/Home-Assistant-Lovelace-HTML-Jinja2-Template-card) to display your data like this:

```yaml
type: vertical-stack
cards:
  - type: entities
    title: Cartão Refeição
    entities:
      - entity: sensor.edenred_card_XXXXXXX
        secondary_info: last-updated
        icon: mdi:credit-card
      - entity: sensor.edenred_card_XXXXXXX
        type: custom:multiple-entity-row
        name: Nome Cartão
        show_state: false
        entities:
          - attribute: ownerName
      - entity: sensor.edenred_card_XXXXXXX
        type: custom:multiple-entity-row
        name: Estado Cartão
        show_state: false
        entities:
          - attribute: cardStatus
  - type: custom:html-template-card
    ignore_line_breaks: true
    content: |
      <table
        style="padding: 0px;border-collapse:separate;
        border:solid gray 1px;
        border-radius:6px;  ">
      <tr>
        <td  colspan="3"><center><font color="#6B8E23" size=4> <b>Últimos Movimentos: </b></center> </font></td>
      </tr>
      <tr>

      </tr>

       <tr>
          <th style="width:10%;"><u><font color=orange>Data</font></u></th>
          <th style="width:65%;"><u><font color=orange>Descrição</font></u></th>
          <th style="width:25%;"><u><font color=orange>Valor</font></u></th>
        </tr> {% for t in state_attr('sensor.edenred_card_XXXXXXX','transactions') %}
          
         <tr>
         <td style="border-top: 1px solid #dddddd;  text-align: center;">{{t.date}}</td> 
         <td style="border-top: 1px solid #dddddd;   text-align: center;">{{t.name}}</td>
         <td style="border-top: 1px solid #dddddd;   text-align: center;"><b>{{t.amount}}</b></td>
      </div></td> 
        </tr>{% endfor %}</table>
```
(credits thanks to [Vítor Nóbrega](https://forum.cpha.pt/u/vpnobrega/summary)).

### Using a custom:list-card

Another alternative is to use [custom:list-card](https://github.com/iantrich/list-card) which has the advantage of being able to indicate the number of rows to display:

```yaml
type: custom:list-card
entity: sensor.edenred_card_XXXXXXX
feed_attribute: transactions
title: MyEdenred Transactions
row_limit: 10
columns:
  - title: Data
    field: date
  - title: Movimento
    field: name
  - title: Valor
    field: amount
    postfix: ' €'
    style:
      - text-align: right
      - white-space: nowrap
```

### Using a custom:browser-mod

If you have [custom:browser-mod](https://github.com/thomasloven/hass-browser_mod) in your sistem, you can show the transactions in a nice popup window, like this:
(this also use [custom:mushroom-entity-card](https://github.com/piitaya/lovelace-mushroom) and [custom:list-card](https://github.com/iantrich/list-card))


```yaml
type: custom:mushroom-entity-card
entity: sensor.edenred_card_XXXXXXX
name: Cartão Refeição
tap_action:
    action: fire-dom-event
    browser_mod:
        command: popup
        title: MyEdenred Transactions
        style:
            .: |
            :host .content {
                width: calc(800px);
                align: center;
            }
        card:
            type: custom:list-card
            entity: sensor.edenred_card_XXXXXXX
            feed_attribute: transactions
            row_limit: 20
            columns:
            - title: Data
                field: date
            - title: Movimento
                field: name
            - title: Valor
                field: amount
                postfix: ' €'
                style:
                - text-align: right
                - white-space: nowrap
            style: |
            tr {
                height: 25px
            }
```

# Legal notice
This is a personal project and isn't in any way affiliated with, sponsored or endorsed by [MyEdenred Portugal](https://www.myedenred.pt/).

All product names, trademarks and registered trademarks in (the images in) this repository, are property of their respective owners. All images in this repository are used by the project for identification purposes only.