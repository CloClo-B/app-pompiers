import React, { useRef } from "react";
import { View } from "react-native";
import { WebView } from "react-native-webview";

interface Props {
  onVerify: (token: string) => void;
}

export default function TurnstileCaptcha({ onVerify }: Props) {

  //Bypass pour éviter les problèmes pendant le dev
  {/*React.useEffect(() => {
    onVerify("token-dev-bypass");
  }, []);
  
  return <View />;*/}

  const webviewRef = useRef<WebView>(null);

  const html = `
    <!DOCTYPE html>
    <html>
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
          body { margin: 0; padding: 10px; background: transparent; display: flex; justify-content: center; }
        </style>
      </head>
      <body>
        <div class="cf-turnstile"
             data-sitekey="1x00000000000000000000AA"
             data-callback="onSuccess"
             data-theme="light">
        </div>
        <script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
        <script>
          function onSuccess(token) {
            window.ReactNativeWebView.postMessage(token);
          }
        </script>
      </body>
    </html>
  `;

  return (
    <View style={{ height: 100, width: '100%' }}>
      <WebView
        ref={webviewRef}
        originWhitelist={["*"]}
        source={{ html }}
        javaScriptEnabled={true}
        domStorageEnabled={true}
        mixedContentMode="always"
        allowUniversalAccessFromFileURLs={true}
        allowFileAccessFromFileURLs={true}
        style={{ backgroundColor: 'transparent' }}
        onMessage={(event) => {
            onVerify(event.nativeEvent.data);
        }}
        />
    </View>
  );
}