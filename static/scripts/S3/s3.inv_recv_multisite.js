/**
 * Used by the inv/recv controller when settings.inv_recv_req = True and there are multiple Sites in the selected Requests
 * - set Sites based on selected Requests
 */

$(document).ready(function() {

    // Set Sites based on selected Requests
    var ajaxURL,
        site,
        fromSites,
        toSites,
        r,
        req_id,
        reqField = $('#link_defaultreq'),
        fromField = $('#inv_recv_from_site_id'),
        toField = $('#inv_recv_site_id');

    var lookupSites = function(req_id) {
        ajaxURL = S3.Ap.concat('/inv/req/recv_sites.json?req_id=' + req_id);
        $.getJSONS3(ajaxURL, function(data) {
            // Clear all options
            fromField.html('');
            toField.html('');
            fromSites = data[0];
            fromSitesLength = fromSites.length;
            if (fromSitesLength) {
                // Add options
                for (var i=0; i < fromSitesLength; i++) {
                    site = fromSites[i];
                    fromField.append(new Option(site[1], site[0]))
                }
                if (fromSitesLength == 1) {
                    // Only a single Site matches, so set to this Site
                    fromField.val(site[0]);
                }
                // Set to 'Internal Shipment'
                $('#inv_recv_type').val(11)
                                   .change();
            }
            toSites = data[1];
            toSitesLength = toSites.length;
            if (toSitesLength == 0) {
                // No Options => No Shipment can be received (e.g. Permissions)
                return;
            }
            // Add options
            for (var i=0; i < toSitesLength; i++) {
                site = toSites[i];
                toField.append(new Option(site[1], site[0]))
            }
            if (toSitesLength == 1) {
                // Only a single Site matches, so set to this Site
                toField.val(site[0]);
            }
        });
    };

    reqField.change(function() {
        req_id = reqField.val();
        lookupSites(req_id);
    });

});