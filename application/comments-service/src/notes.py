        # comments_service_asset = assets.Asset(self, "comments-service-asset",
        #                                       path=f"{dirname}/comments-service/src",
        #                                       bundling=BundlingOptions(
        #                                           image=lambda_.Runtime.PYTHON_3_10.bundling_image,
        #                                           command=["bash", "-c", "pip install -r requirements.txt -t /asset-output && cp -au . /asset-output"
        #                                                    ],
        #                                           security_opt="no-new-privileges:true",
        #                                           network="host"
        #                                       )
        #                                       )
        
                # website_assets = assets.Asset(self, "website-assets",
        #                               path=f"{dirname}/website",
        #                               bundling=BundlingOptions(
        #                                   image=lambda_.Runtime.NODEJS_18_X.bundling_image,
        #                                   command=["bash", "-c", "npm ci && npm run build && cp -aur ./dist/* /asset-output"
        #                                            ],
        #                                   security_opt="no-new-privileges:false",
        #                                   network="host",
        #                                   user="root"
        #                               )
        #                               )