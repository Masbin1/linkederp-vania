/** @odoo-module */
/**
 * Route both the built-in "Print Full Receipt" button AND the automatic
 * print-on-validate (pos.config.autoPrint) to the A4 PDF report instead of
 * the thermal receipt renderer.
 *
 * The PDF is generated server-side, so the order must already be synced —
 * an order created while the POS was offline has no server id yet. In that
 * case the auto-print falls back to the original thermal receipt.
 */

import { ReceiptScreen } from "@point_of_sale/app/screens/receipt_screen/receipt_screen";
import OrderPaymentValidation from "@point_of_sale/app/utils/order_payment_validation";
import { patch } from "@web/core/utils/patch";
import { useTrackedAsync } from "@point_of_sale/app/hooks/hooks";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

const REPORT_XML_ID = "pos_discount_restrict.action_report_pos_order_a4";

patch(ReceiptScreen.prototype, {
    setup() {
        super.setup();
        this.report = useService("report");
        this.doFullPrint = useTrackedAsync(() => this._printA4(this.currentOrder));
    },

    async _printA4(order) {
        if (!order?.isSynced) {
            this.dialog.add(AlertDialog, {
                title: _t("Order Not Synced"),
                body: _t(
                    "This order has not reached the server yet, so the A4 PDF cannot be " +
                        "generated. Check your connection and try again once the order is synced."
                ),
            });
            return;
        }
        return this.report.doAction(REPORT_XML_ID, [order.id]);
    },
});

// The automatic print right after validation (pos.config.autoPrint) also goes
// to the A4 report instead of the thermal receipt. Both manual validate and
// validateOrderFast go through OrderPaymentValidation.afterOrderValidation.
//
// For invoiced orders, core also runs a SEPARATE auto-download in
// finalizeValidation() (step 2, before afterOrderValidation is even called):
// it fetches the real account.move Invoice PDF (e.g. "INV_2026_04568")
// straight from the account_move service — and does it UNCONDITIONALLY,
// with no pos.config.autoPrint check, only order.isToInvoice(). shouldDownloadInvoice()
// below turns that off; afterOrderValidation replaces it with our own report
// on that same unconditional trigger, so an invoiced order still
// auto-downloads even with autoPrint off (matching the native behavior it
// replaces) — it just downloads our A4 report instead of the native invoice.
// Non-invoiced orders keep the normal autoPrint-gated canPrintReceipt path.
patch(OrderPaymentValidation.prototype, {
    shouldDownloadInvoice() {
        return false;
    },

    async afterOrderValidation() {
        if (!this.pos.config.module_pos_restaurant) {
            this.pos.checkPreparationStateAndSentOrderInPreparation(this.order, {
                orderDone: true,
            });
        }

        const order = this.order;
        const shouldAutoDownload = order.isToInvoice() || this.canPrintReceipt;

        if (shouldAutoDownload) {
            // A4 PDF is generated server-side; an offline order has no server id yet.
            if (order.isSynced) {
                await this.pos.env.services.report.doAction(REPORT_XML_ID, [order.id]);
            } else {
                await this.pos.printReceipt({ order });
            }
        }
    },
});
