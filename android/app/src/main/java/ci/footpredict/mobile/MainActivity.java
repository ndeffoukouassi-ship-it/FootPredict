package ci.footpredict.mobile;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebResourceRequest;
import android.content.Intent;
import android.net.Uri;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.view.View;
import android.graphics.Color;

public class MainActivity extends Activity {
    private WebView browser;
    private final String home = "https://footpredict-valentin.onrender.com/";
    @Override public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setBackgroundColor(Color.rgb(15, 23, 42));
        ProgressBar progress = new ProgressBar(this, null, android.R.attr.progressBarStyleHorizontal);
        progress.setIndeterminate(true);
        root.addView(progress, new LinearLayout.LayoutParams(-1, 5));
        browser = new WebView(this);
        root.addView(browser, new LinearLayout.LayoutParams(-1, 0, 1));
        setContentView(root);
        WebSettings settings = browser.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        browser.setWebChromeClient(new WebChromeClient() {
            @Override public void onProgressChanged(WebView view, int newProgress) {
                progress.setVisibility(newProgress >= 100 ? View.GONE : View.VISIBLE);
            }
        });
        browser.setWebViewClient(new WebViewClient() {
            @Override public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                Uri uri = request.getUrl();
                if ("footpredict-valentin.onrender.com".equals(uri.getHost()) && "https".equals(uri.getScheme())) return false;
                try { startActivity(new Intent(Intent.ACTION_VIEW, uri)); } catch (Exception ignored) {}
                return true;
            }
        });
        if (savedInstanceState != null) browser.restoreState(savedInstanceState);
        else browser.loadUrl(home);
    }
    @Override public void onBackPressed() {
        if (browser.canGoBack()) browser.goBack();
        else super.onBackPressed();
    }
    @Override protected void onSaveInstanceState(Bundle state) { browser.saveState(state); super.onSaveInstanceState(state); }
    @Override protected void onDestroy() { if (browser != null) browser.destroy(); super.onDestroy(); }
}
